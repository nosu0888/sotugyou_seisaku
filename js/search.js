const foodMenu = {
  "japaneseFoods": ["寿司", "天ぷら", "おでん"],
  "chineseFoods": ["八宝菜", "麻婆豆腐", "エビチリ"],
  "italianFoods": ["パスタ", "ピザ", "ミネストローネ"]
};


function createMenu(selectGenre) {

  let menuList = document.getElementById('menuList');
  menuList.disabled = false;
  menuList.innerHTML = '';
  let option = document.createElement('option');
  option.innerHTML = '料理を選択してください';
  option.defaultSelected = true;
  option.disabled = true;
  menuList.appendChild(option);

  foodMenu[selectGenre].forEach(menu => {
    let option = document.createElement('option');
    option.innerHTML = menu;
    menuList.appendChild(option);
  });
}