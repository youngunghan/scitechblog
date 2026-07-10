#!/usr/bin/env bash

set -euo pipefail

if [ -f package.json ]; then
  bash -i -c \
    "nvm install && nvm use && npm ci --ignore-scripts && ./node_modules/.bin/husky && npm run build"
fi

# Install dependencies for shfmt extension
case "$(uname -m)" in
x86_64)
  shfmt_arch="amd64"
  shfmt_sha256="d9fbb2a9c33d13f47e7618cf362a914d029d02a6df124064fff04fd688a745ea"
  ;;
aarch64 | arm64)
  shfmt_arch="arm64"
  shfmt_sha256="5f3fe3fa6a9f766e6a182ba79a94bef8afedafc57db0b1ad32b0f67fae971ba4"
  ;;
*)
  echo "Unsupported architecture for shfmt: $(uname -m)" >&2
  exit 1
  ;;
esac

shfmt_tmp="$(mktemp)"
curl --fail --location --silent --show-error \
  "https://github.com/mvdan/sh/releases/download/v3.12.0/shfmt_v3.12.0_linux_${shfmt_arch}" \
  --output "$shfmt_tmp"
echo "$shfmt_sha256  $shfmt_tmp" | sha256sum --check --status
sudo install -m 0755 "$shfmt_tmp" /usr/local/bin/shfmt
rm -f "$shfmt_tmp"

# Add OMZ plugins
if [ ! -d ~/.oh-my-zsh/custom/plugins/zsh-syntax-highlighting ]; then
  git clone --branch 0.8.0 --depth 1 https://github.com/zsh-users/zsh-syntax-highlighting.git \
    ~/.oh-my-zsh/custom/plugins/zsh-syntax-highlighting
fi
test "$(git -C ~/.oh-my-zsh/custom/plugins/zsh-syntax-highlighting rev-parse HEAD)" = \
  "db085e4661f6aafd24e5acb5b2e17e4dd5dddf3e"
if [ ! -d ~/.oh-my-zsh/custom/plugins/zsh-autosuggestions ]; then
  git clone --branch v0.7.1 --depth 1 https://github.com/zsh-users/zsh-autosuggestions \
    ~/.oh-my-zsh/custom/plugins/zsh-autosuggestions
fi
test "$(git -C ~/.oh-my-zsh/custom/plugins/zsh-autosuggestions rev-parse HEAD)" = \
  "e52ee8ca55bcc56a17c828767a3f98f22a68d4eb"
sed -i -E "s/^(plugins=\()(git)(\))/\1\2 zsh-syntax-highlighting zsh-autosuggestions\3/" ~/.zshrc

# Avoid git log use less
printf '\nunset LESS\n' >>~/.zshrc
