module.exports = {
  site: 'gguide.com',
  channels: 'channels.xml',
  output: 'public/epg.xml',
  days: 1,
  url: function ({ channel, date }) {
    return `https://bangumi.org/epg/td?channel=${channel.site_id}&date=${date.format('YYYYMMDD')}`;
  },
  parser: function ({ content }) {
    return [];
  }
};
