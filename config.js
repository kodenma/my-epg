module.exports = {
  site: 'gguide.com',
  days: 1,
  url: function ({ channel, date }) {
    // 取得先URLを動的に生成する関数
    return `https://bangumi.org/epg/td?channel=${channel.site_id}&date=${date.format('YYYYMMDD')}`;
  },
  parser: function ({ content }) {
    // 番組表解析ロジック（空配列を返す初期定義）
    return [];
  }
};
