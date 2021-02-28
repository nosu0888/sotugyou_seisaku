< html >
  <
  head >
  <
  title > TAG index Webサイト < /title>

  <
  script type = "text/javascript" >
  <
  !--

function disp() {

  // 「OK」時の処理開始 ＋ 確認ダイアログの表示
  if (window.confirm('本当にいいんですね？')) {

    location.href = "example_confirm.html"; // example_confirm.html へジャンプ

  }
  // 「OK」時の処理終了

  // 「キャンセル」時の処理開始
  else {

    window.alert('キャンセルされました'); // 警告ダイアログを表示

  }
  // 「キャンセル」時の処理終了

}

// -->
<
/script>

<
/head> <
body >

  <
  p > < input type = "button"
value = "確認ダイアログ"
onClick = "disp()" > < /p>

  <
  /body> < /
  html >