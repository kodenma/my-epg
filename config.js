const cheerio = require('cheerio');
const dayjs = require('dayjs');

// channels.xml の ID と Gガイド(bangumi.org) 放送局IDの対応表（関東主要局）
const CHANNEL_MAP = {
  'NHKGeneral.jp': '101016', // NHK総合
  'EETV.jp':       '101024', // Eテレ
  'NTV.jp':        '101040', // 日本テレビ
  'TVAsahi.jp':    '101048', // テレビ朝日
  'TBS.jp':        '101056', // TBS
  'TVTokyo.jp':    '101072', // テレビ東京
  'FujiTV.jp':     '101064'  // フジテレビ
};

module.exports = {
  site: 'gguide.com',
  channels: 'channels.xml',
  output: 'public/epg.xml',
  days: 1,
  request: {
    headers: {
      'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
  },
  url: function ({ channel }) {
    const siteId = CHANNEL_MAP[channel.site_id] || channel.site_id;
    return `https://bangumi.org/epg/td?gg_id=${siteId}`;
  },
  parser: function ({ content }) {
    const $ = cheerio.load(content);
    const programs = [];

    // Gガイドの番組枠要素から情報を抽出
    $('.cell-schedule, .program, [data-start]').each((_, el) => {
      const $item =$(el);
      const title = $item.find('.title, .program_title, a').first().text().trim();
      const desc = $item.find('.detail, .desc, .summary').text().trim();
      const startTime = $item.attr('data-start');
      const stopTime = $item.attr('data-stop');

      if (title && startTime && stopTime) {
        programs.push({
          title: title,
          description: desc,
          start: dayjs(startTime),
          stop: dayjs(stopTime)
        });
      }
    });

    return programs;
  }
};
