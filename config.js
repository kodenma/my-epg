const cheerio = require('cheerio');
const dayjs = require('dayjs');
const customParseFormat = require('dayjs/plugin/customParseFormat');
const timezone = require('dayjs/plugin/timezone');
const utc = require('dayjs/plugin/utc');

dayjs.extend(utc);
dayjs.extend(timezone);
dayjs.extend(customParseFormat);

module.exports = {
  site: 'gguide.com',
  channels: 'channels.xml',
  output: 'public/epg.xml',
  days: 1,
  request: {
    headers: {
      'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
      'Accept-Language': 'ja,en-US;q=0.9,en;q=0.8'
    }
  },
  url: function ({ channel, date }) {
    // 局コードをそのままURLパラメータに渡す
    return `https://bangumi.org/epg/td?gg_id=${channel.site_id}`;
  },
  parser: function ({ content, date }) {
    const $ = cheerio.load(content);
    const programs = [];
    const baseDate = dayjs(date).format('YYYY-MM-DD');

    // bangumi.org の番組リンク要素（.program-title やリンクなど）を走査
    // ※サイトのHTML構造に合わせてクラス名を調整
    $('article, .program, [class*="schedule"]').each((_, el) => {
      const $item = $(el);
      const title = $item.find('h1, h2, h3, .title, a').first().text().trim();
      const desc = $item.find('p, .detail, .desc').first().text().trim();
      
      // 時間情報の取得（例: 05:00〜05:30 などのテキストを抽出）
      const timeText = $item.find('.time, [class*="time"]').text().trim();
      const match = timeText.match(/(\d{1,2}):(\d{2})\s*[〜~-]\s*(\d{1,2}):(\d{2})/);

      if (title && match) {
        const start = dayjs.tz(`${baseDate} ${match[1]}:${match[2]}`, 'YYYY-MM-DD HH:mm', 'Asia/Tokyo');
        let stop = dayjs.tz(`${baseDate} ${match[3]}:${match[4]}`, 'YYYY-MM-DD HH:mm', 'Asia/Tokyo');
        
        // 日付をまたぐ場合の補正
        if (stop.isBefore(start)) {
          stop = stop.add(1, 'day');
        }

        programs.push({
          title: title,
          description: desc,
          start: start,
          stop: stop
        });
      }
    });

    return programs;
  }
};
