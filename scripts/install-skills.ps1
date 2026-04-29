#!/usr/bin/env pwsh
# install-skills.ps1
# 在 Codex CLI 中运行本脚本对应的命令，安装推荐的官方精选 Skills
# 使用方式：在 Codex 会话中，直接粘贴下方命令

Write-Host "================================================" -ForegroundColor Cyan
Write-Host " Code Review Agent — 推荐 Skills 安装指南" -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "请在 Codex CLI 或 Codex App 中依次执行以下命令：" -ForegroundColor Yellow
Write-Host ""

Write-Host "【必装 - 高频使用】" -ForegroundColor Green
Write-Host '  $skill-installer pdf'
Write-Host '  $skill-installer jupyter-notebook'
Write-Host '  $skill-installer openai-docs'
Write-Host ""

Write-Host "【项目开发 - 强烈推荐】" -ForegroundColor Green
Write-Host '  $skill-installer gh-address-comments'
Write-Host '  $skill-installer gh-fix-ci'
Write-Host '  $skill-installer playwright'
Write-Host '  $skill-installer screenshot'
Write-Host ""

Write-Host "【文档与调研输出】" -ForegroundColor Green
Write-Host '  $skill-installer notion-research-documentation'
Write-Host '  $skill-installer doc'
Write-Host ""

Write-Host "【代码分析与安全】" -ForegroundColor Green
Write-Host '  $skill-installer security-best-practices'
Write-Host '  $skill-installer security-ownership-map'
Write-Host '  $skill-installer security-threat-model'
Write-Host ""

Write-Host "【可选 - 部署相关】" -ForegroundColor Yellow
Write-Host '  $skill-installer vercel-deploy'
Write-Host '  $skill-installer render-deploy'
Write-Host ""

Write-Host "================================================" -ForegroundColor Cyan
Write-Host "安装完成后，重启 Codex 以加载新 Skills。" -ForegroundColor Yellow
Write-Host "本项目的自定义 Skills 已自动在 .agents/skills/ 中配置好，" -ForegroundColor Yellow
Write-Host "无需额外安装，Codex 启动时会自动发现。" -ForegroundColor Yellow
Write-Host "================================================" -ForegroundColor Cyan
