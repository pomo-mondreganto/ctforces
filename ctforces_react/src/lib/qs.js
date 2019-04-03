import queryString from 'query-string';

export default s => queryString.parse(s, { ignoreQueryPrefix: true });
