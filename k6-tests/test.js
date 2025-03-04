import http from 'k6/http';
import { check, sleep } from 'k6';

export let options = {
  stages: [
    { duration: '30s', target: 10 },  // 30 秒內提升到 10 個 VUs
    { duration: '1m', target: 50 },   // 接著 1 分鐘內提升到 50 個 VUs
    { duration: '30s', target: 0 },   // 30 秒內逐步降低到 0 VUs
  ],
};

export default function () {
  let res = http.get('https://www.saucedemo.com/');
  check(res, {
    '狀態碼為 200': (r) => r.status === 200,
  });
  sleep(1); // 每個請求間隔 1 秒
}