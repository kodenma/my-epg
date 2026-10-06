const cheerio = require('cheerio');
const dayjs = require('dayjs');

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
  url: function ({ channel, date }) {
    // channels.xml の site_id をそのまま利用
    // 日付指定が必要な場合はクエリパラメータを追加 (例: &date=YYYYMMDD)
    const targetDate = dayjs(date).format('YYYYMMDD');
    return `https://bangumi.org/epg/td?gg_id=${channel.site_id}&date=${targetDate}`;
  },
  parser: function ({ content, date }) {
    const $ = cheerio.load(content);
    const programs = [];

    // ※実際のHTMLソースに合わせてセレクタ・属性名を調整してください
    $('.cell-schedule, .program, [data-start]').each((_, el) => {
      const $item = $(el);
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
