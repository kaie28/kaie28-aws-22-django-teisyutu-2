# 1. プロバイダー設定
provider "aws" {
  region = "ap-northeast-1"
}

# 名前の指定を確実にヒットする形に変更
data "aws_ami" "recent_amazon_linux_2023" {
  most_recent = true
  owners      = ["amazon"]

  filter {
    name   = "name"
    # 「al2023-ami-」で始まって「x86_64」で終わるものを探す
    values = ["al2023-ami-*-x86_64"] 
  }
}


# 2. ネットワーク (VPC)
resource "aws_vpc" "main" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_support   = true
  enable_dns_hostnames = true
  tags = { Name = "todo-vpc" }
}

# 3. インターネット接続 (IGW)
resource "aws_internet_gateway" "gw" {
  vpc_id = aws_vpc.main.id
  tags   = { Name = "todo-igw" }
}

# 4. サブネット
resource "aws_subnet" "public" {
  vpc_id                  = aws_vpc.main.id
  cidr_block              = "10.0.1.0/24"
  map_public_ip_on_launch = true
  availability_zone       = "ap-northeast-1a"
  tags                    = { Name = "todo-subnet" }
}

# 5. ルートテーブル (外の世界と繋ぐ)
resource "aws_route_table" "rt" {
  vpc_id = aws_vpc.main.id
  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.gw.id
  }
}

resource "aws_route_table_association" "a" {
  subnet_id      = aws_subnet.public.id
  route_table_id = aws_route_table.rt.id
}

# 6. セキュリティグループ (22番SSHを自分のIPからのみ許可)
resource "aws_security_group" "sg" {
  name   = "ssh-only-sg"
  vpc_id = aws_vpc.main.id


 # 自分用で外からサーバーへ*設定
ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    # ここを自分のIPアドレスに書き換え（例: "123.456.78.9/32"）
    cidr_blocks = ["193.186.4.180/32"] 
  }

  # お客さん用の外からサーバーへ*設定
  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"] # 全員に公開
  }


# サーバーから外へ出る**ための設定
egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}


# 7. SSM (ブラウザ接続) 用の権限設定
resource "aws_iam_role" "ssm_role" {
  name = "todo-ssm-role"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action = "sts:AssumeRole"
      Effect = "Allow"
      Principal = { Service = "ec2.amazonaws.com" }
    }]
  })
}


# B. AWSが用意している「SSM用テンプレート」
resource "aws_iam_role_policy_attachment" "ssm_attach" {
  role       = aws_iam_role.ssm_role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonSSMManagedInstanceCore"
}
# C. インスタンスに「許可証」をセットするための器を作る
resource "aws_iam_instance_profile" "ssm_profile" {
  name = "todo-ssm-profile"
  role = aws_iam_role.ssm_role.name

}


# 8. EC2インスタンス (Nginxのみ自動インストール)
# D. EC2インスタンス作成時に、このプロファイルを指定する
resource "aws_instance" "kaie28" {
 
  ami                  = data.aws_ami.recent_amazon_linux_2023.id
  instance_type        = "t3.micro"
  subnet_id            = aws_subnet.public.id
  iam_instance_profile = aws_iam_instance_profile.ssm_profile.name
  vpc_security_group_ids = [aws_security_group.sg.id]
  
  # AWSコンソールにある正式な名前で入力
  key_name = "my-ssh-key" 

  # 初期セットアップ（Nginxのインストールまで）
  user_data = <<-EOF
              #!/bin/bash
              dnf update -y
              dnf install -y nginx
              systemctl start nginx
              systemctl enable nginx
              EOF

  tags = { Name = "kaie28" }
}

