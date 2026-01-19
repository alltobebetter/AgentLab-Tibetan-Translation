// Vercel Serverless Function - 藏文翻译API
import { parse } from 'node-html-parser';

export default async function handler(req, res) {
  // 只允许POST请求
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  try {
    const { text, direction = 'tc' } = req.body;

    // 参数验证
    if (!text) {
      return res.status(400).json({ error: '缺少text参数' });
    }

    if (!['tc', 'ct'].includes(direction)) {
      return res.status(400).json({ 
        error: 'direction必须是tc(藏→中)或ct(中→藏)' 
      });
    }

    // 调用西藏大学翻译API
    const formData = new URLSearchParams();
    formData.append('src', text);
    formData.append('lang', direction);

    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), 25000);

    const response = await fetch('https://nmt.utibet.edu.cn/mt', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
      },
      body: formData.toString(),
      signal: controller.signal
    });

    clearTimeout(timeoutId);

    if (!response.ok) {
      throw new Error(`HTTP ${response.status}`);
    }

    const html = await response.text();
    
    // 解析HTML获取翻译结果
    const root = parse(html);
    const resultTextarea = root.querySelector('textarea#txt2[name="tgt"]');
    
    if (!resultTextarea) {
      throw new Error('未找到翻译结果');
    }

    const translation = resultTextarea.text.trim();

    if (!translation) {
      throw new Error('翻译结果为空');
    }

    // 返回结果
    return res.status(200).json({
      success: true,
      source: text,
      translation: translation,
      direction: direction,
      directionName: direction === 'tc' ? '藏文→中文' : '中文→藏文'
    });

  } catch (error) {
    console.error('Translation error:', error);
    return res.status(500).json({
      success: false,
      error: error.message || '翻译失败'
    });
  }
}
