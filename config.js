const cheerio = require('cheerio');
const dayjs = require('dayjs');

module.exports = {
  site: 'gguide.com',
  channels: 'channels.xml',
  output: 'public/epg.xml',
  days: 1,
  url: function ({ channel }) {
    // Gガイド（bangumi.org）の番組表ページを取得
    return `https://bangumi.org/epg/td?gg_id=${channel.site_id}`;
  },
  parser: function ({ content, date }) {
    const $ = cheerio.load(content);
    const programs = [];

    // HTML要素から番組情報を抽出
    $('.cell-schedule').each((_, el) => {
      const $item =$(el);
      const title = $item.find('.title').text().trim();
      const desc = $item.find('.detail, .desc').text().trim();
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
