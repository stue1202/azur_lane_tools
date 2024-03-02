<template>
  <v-app>
    <v-app-bar :elevation="2">
      <template v-slot:prepend>
        <v-app-bar-nav-icon @click="show_navbar = !show_navbar"></v-app-bar-nav-icon>
      </template>

      <v-app-bar-title>碧藍配對模擬</v-app-bar-title>
      <v-btn icon><v-icon icon="mdi-cog"></v-icon></v-btn>
      <v-btn icon v-show="!is_signin" @click="show_login = true"><v-icon icon="mdi-account"></v-icon></v-btn>
      <v-btn icon v-show="is_signin"><v-avatar><v-img :src=user_info.avatar></v-img></v-avatar></v-btn>
    </v-app-bar>
    <v-navigation-drawer v-model="show_navbar">
      <v-list>

        <v-list-item link :variant="big_fleet_index === nowselect.big_fleet_index ? 'tonal' : ''"
          :title="item.big_fleet_name + ':' + big_fleet_index" v-for="(item, big_fleet_index) in user_info.user_fleet"
          @click="nowselect.big_fleet_index = big_fleet_index"></v-list-item>
        <v-list-item link title="+" style="text-align: center" @click="show_big_fleet_naming = true"></v-list-item>
      </v-list>

    </v-navigation-drawer>
    <!--login-->
    <v-dialog width="400" v-model="show_login">
      <v-card title="login or signup">
        <v-container class="py-10 text-center">
          <v-text-field v-model="user_info.username" label="帳號" type="email" class="mb-5"></v-text-field>
          <v-text-field v-model="user_info.password" label="密碼" type="password" class="mb-5"></v-text-field>
          <v-text-field v-model="user_info.password" label="密碼確認" type="password" class="mb-5"
            v-if="signup"></v-text-field>
          <v-row>
            <v-col cols="6"><v-btn type="submit" color="primary" @click="login">登入</v-btn></v-col>
            <v-col cols="6"><v-btn type="submit" color="primary" @click="signup(); signup = true">註冊</v-btn></v-col>
          </v-row>
          <v-divider class="my-10"></v-divider>
          <GoogleLogin :callback="Google_Login" />
        </v-container>
      </v-card>
    </v-dialog>

    <!--add big_fleet-->
    <v-dialog width="400" v-model="show_big_fleet_naming" persistent>
      <v-card title="為大艦隊命名">
        <v-container>
          <v-text-field v-model="big_fleet_name"></v-text-field>
          <v-spacer></v-spacer>
          <v-card-actions>
            <v-btn @click="show_big_fleet_naming = false">取消</v-btn>
            <v-btn color="primary" @click="add_big_fleet(big_fleet_name)">確認</v-btn>

          </v-card-actions>
        </v-container>
      </v-card>
    </v-dialog>


    <!--shippicker-->


    <v-dialog width="1000" v-model="show_shippicker">


      <v-card title="shippicker">
        <v-container>
          <v-row class="pa-10">
            <v-col>
              <v-autocomplete label="陣營"
                :items="['全部', '白鷹', '皇家', '東煌', '北方聯合', '鐵血', '自由鳶尾', '維希教廷', '薩丁帝國', '重櫻', '連動', '其他']" variant="outlined"
                v-model="ship_fliter.team"></v-autocomplete>
            </v-col>
            <v-col>
              <v-autocomplete label="稀有度" :items="['全部', '普通', '稀有', '精銳', '超稀有', '海上傳奇', '最高方案']" variant="outlined"
                v-model="ship_fliter.rare"></v-autocomplete>
            </v-col>
            <v-col>
              <!--前排-->
              <v-autocomplete v-if="nowselect.ship_index > 3" label="類型" :items="['全部', '驅逐', '輕巡', '重巡', '超巡']"
                variant="outlined" v-model="ship_fliter.shiptype"></v-autocomplete>
              <!--後排-->
              <v-autocomplete v-else label="類型" :items="['全部', '戰巡', '戰列', '航母', '輕航', '重砲', '維修']" variant="outlined"
                v-model="ship_fliter.shiptype"></v-autocomplete>
            </v-col>
          </v-row>
          <!--show all ship start-->

          <v-row class="mt-n10">

            <v-col v-for="(item, index) in shiplist.filter(ship => {
              if (ship.shipname === '移除') {
                return true
              }
              if (ship_fliter.rare !== '全部' && ship_fliter.rare !== ship.rare) {
                return false
              }
              if (ship_fliter.team !== '全部' && ship_fliter.team !== ship.team) {
                return false
              }
              if (ship_fliter.shiptype !== '全部' && ship_fliter.shiptype !== ship.shiptype) {
                return false
              }
              if (nowselect.ship_index > 2 && ship.front_or_back !== '前排先鋒') {
                return false
              }
              if (nowselect.ship_index < 3 && ship.front_or_back !== '後排主力') {
                return false
              }
              return true
            })" cols="1" class="text-center pa-1 overflow-hidden" style="height:100px">

              <v-img :style="{border: ' 1.5px solid ' + diciding_border(item.rare)}" :src="item.iconsrc" :title="item.shipname"
                @click="set_chosen_ship(item)"></v-img>
              <h5>{{ item.shipname }}</h5>
            </v-col>
          </v-row>

          <!--show all ship end-->
        </v-container>
      </v-card>

    </v-dialog>

    <!--shippicker end-->

    <v-main><v-container v-if="user_info.user_fleet.length > 0">
        <v-row v-if="edit_big_fleet">
          <v-col cols="6" class="text-center" style="border: 1px solid blue;">
            <v-text-field v-model="tmp" @keyup.enter="user_info.user_fleet[nowselect.big_fleet_index].big_fleet_name = tmp"
              color="primary" label="大艦隊名稱" variant="underlined"></v-text-field>
          </v-col>
          <v-col cols="3" class="text-center" style="border: 1px solid blue;">
            <v-btn color="red"
              @click="() => { user_info.user_fleet.splice(nowselect.big_fleet_index, 1); nowselect.big_fleet_index = 0 }">刪除此艦隊</v-btn>
          </v-col>
          <v-col cols="3" class="text-center" style="border: 1px solid blue;">
            <v-btn color="red"
              @click="() => { tmp = nowselect.big_fleet_index; user_info.user_fleet.unshift(user_info.user_fleet[nowselect.big_fleet_index]); user_info.user_fleet.splice(tmp + 1, 1); nowselect.big_fleet_index = 0 }">移至最上方</v-btn>
          </v-col>
        </v-row>
        <v-container class="d-flex flex-wrap justify-center">
          
          <!--shipcard start-->
          <v-card v-for="(shipcards, card_index) in user_info.user_fleet[nowselect.big_fleet_index].shipcards"
            :key="card_index" :width="400" class="ma-7">
            <v-container>
              <v-row>
                <v-col cols="4" style="height: 140px;" class="overflow-hidden" v-for="(ship,ship_index) in shipcards.little_fleet">
                  <v-img :style="{border: ' 1.5px solid ' + diciding_border(ship.rare)}" class="text-center" @click="select_ship(card_index, ship_index)"
                    :src=ship.iconsrc></v-img>
                  <h5>{{ship.shipname}}</h5>
                </v-col>
              </v-row>
              <v-spacer></v-spacer>
              <v-card-actions>
                <v-btn v-if="edit_big_fleet"
                  @click="user_info.user_fleet[nowselect.big_fleet_index].shipcards.splice(card_index, 1)"
                  color="red">刪除</v-btn>
              </v-card-actions>
            </v-container>
          </v-card>

          <!--shipcard end-->
        </v-container>
        <v-btn @click="add_shipcards" icon color="blue" style=" position: fixed; bottom: 20px; right: 20px; "><v-icon
            icon="mdi-plus"></v-icon></v-btn>
        <v-btn @click="edit_big_fleet = !edit_big_fleet" icon color="red"
          style=" position: fixed; bottom: 85px; right: 20px; "><v-icon icon="mdi-pen"></v-icon></v-btn>


        <v-btn @click="console.log(shiplist)">dev</v-btn>


      </v-container></v-main>
  </v-app>
</template>

<script setup>
import { ref, reactive } from 'vue'
import axios from 'axios'
import { onMounted, watchEffect } from 'vue';

const tmp = ref('')
const edit_big_fleet = ref(false)
const is_signin = ref(false)
const show_navbar = ref(true)
const show_login = ref(false)
const show_big_fleet_naming = ref(false)
const ship_fliter = reactive({ shiptype: '全部', rare: '全部', team: '全部' })
const show_shippicker = ref(false)
const shiplist = reactive([])
const nowselect = reactive({ big_fleet_index: '0', card_index: "", ship_index: "" })
const user_info = reactive({ username: '', password: '', avatar: '', user_fleet: [], id: '' })
const border_table = reactive({ 普通: 'gray', 稀有: '#5C96CF', 精銳: 'purple', 超稀有: '#CFC45C', 海上傳奇: 'red', 最高方案: 'red' })
const init_little_fleet = reactive({
  "shipname": "移除",
  "iconsrc": "https://pic.616pic.com/ys_bnew_img/00/12/44/xEkMg3S2xa.jpg",
  "rare": "all",
  "shiptype": "all",
  "team": "all",
  "front_or_back": "all"
})
const diciding_border=(rare)=>{
  return border_table[rare]
}
const fliter = reactive({ rare: "", type: "", team: "" })
const select_ship = (card_index, ship_index) => {
  show_shippicker.value = true
  nowselect.card_index = card_index
  nowselect.ship_index = ship_index
  ship_fliter.shiptype = '全部'
}
const set_chosen_ship = (item) => {
  user_info.user_fleet[nowselect.big_fleet_index].shipcards[nowselect.card_index].little_fleet[nowselect.ship_index] = item
  show_shippicker.value = false
}
const add_big_fleet = (name) => {
  if (user_info.user_fleet.find((fleet) => { return fleet.big_fleet_name === name }) || name.trim() === '') {
    window.alert("名稱不要重複或空白")
  }
  else {
    user_info.user_fleet.push({ big_fleet_name: name, shipcards: [{ little_fleet_name: "new", little_fleet: [init_little_fleet, init_little_fleet, init_little_fleet, init_little_fleet, init_little_fleet, init_little_fleet] }] })
    show_big_fleet_naming.value = false
  }
}
const add_shipcards = () => {
  user_info.user_fleet[nowselect.big_fleet_index].shipcards.push({ little_fleet_name: "new", little_fleet: [init_little_fleet, init_little_fleet, init_little_fleet, init_little_fleet, init_little_fleet, init_little_fleet] })
}
const login = () => {
  console.log(user_info)
  if (0) {
    window.alert("輕輸入完整")
  } else {
    axios.post('http://127.0.0.1:5000/login', user_info)
      .then(response => {
        const result = response.data;

      })
      .catch(error => {
        console.error('Error fetching data:', error);
      });
  }
}
const Google_Login = (response) => {
  axios.post('http://127.0.0.1:5000/google_login', response)
    .then(response => {
      const result = response.data;
      console.log(result)
      if (result !== 'error') {
        is_signin.value = true
        show_login.value = false
        user_info.id = result.id
        user_info.avatar = result.avatar
        user_info.username = result.username
        user_info.user_fleet = result.user_fleet
        localStorage.setItem('user_id', user_info.id)
      }
    })
}
watchEffect(() => {
  if (is_signin) {
    axios.post('http://127.0.0.1:5000/upload', user_info)// 處理從後端獲取的 JSON 數據
      .then(response => {

      })
      .catch(error => {
        console.error('Error fetching data:', error);
      });
  }
})

onMounted(() => {
  try {
    const id = localStorage.getItem('user_id')
    console.log(id)

  } catch {

  }
  axios.get('http://127.0.0.1:5000/getshipinfo')// 處理從後端獲取的 JSON 數據
    .then(response => {
      const temp_data = response.data;
      shiplist.push(init_little_fleet)
      temp_data.forEach(element => {
        shiplist.push({ shipname: element[5], iconsrc: element[4], rare: element[2], shiptype: element[1], team: element[3], front_or_back: element[0] })
      });
    })
    .catch(error => {
      console.error('Error fetching data:', error);
    });
})

</script>

<style></style>