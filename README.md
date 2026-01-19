# AgentLab Tibetan Translation API

A serverless Tibetan-Chinese neural machine translation API built with Vercel.

## Overview

This project provides a REST API for bidirectional translation between Tibetan and Chinese languages. The API is deployed as a serverless function on Vercel, offering fast and scalable translation services.

## Features

- **Bidirectional Translation**: Supports both Tibetan→Chinese and Chinese→Tibetan
- **Serverless Architecture**: Deployed on Vercel with automatic scaling
- **RESTful API**: Simple JSON-based API interface
- **CORS Enabled**: Can be accessed from any domain
- **Lightweight**: No database required, stateless design

## API Endpoint

```
POST /api/translate
```

### Request

```json
{
  "text": "བཀྲ་ཤིས་བདེ་ལེགས།",
  "direction": "tc"
}
```

### Response

```json
{
  "success": true,
  "source": "བཀྲ་ཤིས་བདེ་ལེགས།",
  "translation": "扎西德勒",
  "direction": "tc",
  "directionName": "藏文→中文"
}
```

## Parameters

- `text` (required): Text to be translated
- `direction` (optional): Translation direction
  - `tc`: Tibetan → Chinese (default)
  - `ct`: Chinese → Tibetan

## Tech Stack

- **Runtime**: Node.js (Vercel Serverless Functions)
- **Parser**: node-html-parser
- **Deployment**: Vercel
- **Translation Engine**: Tibet University's Sunshine NMT System

## Project Structure

```
.
├── api/
│   └── translate.js       # Serverless function
├── public/
│   ├── index.html         # API documentation page
│   └── favicon.svg        # Site icon
├── package.json           # Node.js dependencies
└── vercel.json           # Vercel configuration
```

## Acknowledgments

Translation service powered by Tibet University's Sunshine Tibetan-Chinese Machine Translation System.

## License

© 2026 AgentLab
