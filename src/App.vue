<!--主介面和登入-->
<template class="scroll-container">
  <div>
    <div id="titlebar">
    <h1>碧藍航線配隊工具</h1>
    <div v-if="!is_sign_in">
      <button @click="show_login_windows(true)">登入</button>
    </div>
    <div v-if="is_sign_in">
      <h5>歡迎{{ Userinfo.userid }}</h5>
      <button @click="log_out()">登出</button>
    </div>
    
    
  </div>
    <input v-model="fleetname" @keyup.enter="add_fleet" placeholder="輸入隊伍名稱" />

    <ul>
      <li v-for="(item,index) in fleet_list" :key="item.index">
        <div>
          name: {{ item.name }}
          <button @click="remove_fleet(index)">刪除</button>
        </div>
         <!--網格-->
        <div id="shipgrid">
            <img :src="getButtom_style(5,index)" @click="open_ship_list(5,index)" class="ship">
            <img :src="getButtom_style(4,index)" @click="open_ship_list(4,index)" class="ship">
            <img :src="getButtom_style(3,index)" @click="open_ship_list(3,index)" class="ship">

            <img :src="getButtom_style(2,index)" @click="open_ship_list(2,index)" class="ship">
            <img :src="getButtom_style(1,index)" @click="open_ship_list(1,index)" class="ship">
            <img :src="getButtom_style(0,index)" @click="open_ship_list(0,index)" class="ship">
        </div>
       
      </li>
    </ul>
  </div>
  <button @click="close_ship_list" id="close_ship_list" v-if="show_shiplist">X</button>
    <!--彈出式選單-->
    <!--篩選部分-->
    <div v-if="show_shiplist" id="popup_shiplist">  
            <div id="fliter">
            陣營：
            <select>
                <option>ALL</option>
                <option>US</option>
                <option>EN</option>
                <option>CH</option>
                <option>FR</option>
                <option>IT</option>
                <option>RU</option>
                <option>DE</option>
                <option>OTHER</option>
            </select>
            等級: 
            <select>
                <option>ALL</option>
                <option>1</option>
                <option>2</option>
                <option>3</option>
                <option>4</option>
                <option>5</option>
                <option>6</option>
            </select>
            <button>清除</button>
        </div>
        <!--載入所有船-->
        <div id="shipsort">
            <div v-for="(item,index) in ship_data" :key=index class="shipitem" @click="chosen_character(item)">
              <img :src="require(`@/assets/shipicon/${item.shipname}.png`)" />
                <div>{{ item.shipname }}</div>
            </div>
        </div> 
    </div>
    <div v-if="show_login_windows_val" id="popup_login">  
            <div>登入</div>
            <input type="text" v-model="Userinfo.userid">
            <input type="password" v-model="Userinfo.userpassword">
            <button @click="login()">登入</button>
            <button @click="sign_up()">註冊</button>
            <button @click="show_login_windows(false)">取消</button>
    </div>
</template>

<script setup>
import { ref, reactive,onMounted, watchEffect } from 'vue';
import axios from 'axios';

const Userinfo=ref({userid:'',userpassword:''})
const is_sign_in=ref(false);

const fleetname = ref('');
const fleet_list = reactive([]);


const show_shiplist = ref(false);
const chosen_buttonid=ref(0);
const chosen_fleet_index=ref(0);

const show_login_windows_val=ref(false);
const show_login_windows=(r)=>{
  show_login_windows_val.value=r;
}


//登入登出
const log_out=()=>{
  Userinfo.value.userpassword='';
  Userinfo.value.userid='';
  fleet_list.length=0;
  is_sign_in.value=false;
}

const login=()=>{
  if(Userinfo.value.userid.trim()!=='' && Userinfo.value.userpassword.trim()!==''){
    window.alert("name: "+Userinfo.value.userid+" password: "+Userinfo.value.userpassword);
    axios.post('http://localhost:8081/login',{userid:Userinfo.value.userid,userpassword:Userinfo.value.userpassword},
  {
    headers: {
      'Content-Type': 'application/json',
    },
    responseType: 'json' 
  }).then(Response=>{
    fleet_list.length=0;
    Response.data.forEach(item=>{
      fleet_list.push(item);
    })
    is_sign_in.value=true;
    show_login_windows_val.value=false;
    }).catch(error=>{
      window.alert("無法登入："+error.toString());
      console.log(error);
    })
    
  }
  else{
    window.alert("請輸入完整");
  }
}

const sign_up=()=>{
  if(Userinfo.value.userid.trim()!=='' && Userinfo.value.userpassword.trim()!==''){
    window.alert("name: "+Userinfo.value.userid+" password: "+Userinfo.value.userpassword);
    axios.post('http://localhost:8081/sign_up',{userid:Userinfo.value.userid,userpassword:Userinfo.value.userpassword}, // 数据
  {
    headers: {
      'Content-Type': 'application/json', // 请求头
      // 其他请求头配置
    },
    responseType: 'json' 
  }).then(Response=>{
    console.log(Response.toString)
    }).catch(error=>{
      window.alert("無法註冊："+error.toString());
      console.log(error);
    })

  }
  else{
    window.alert("請輸入完整");
  }
}
watchEffect(()=>{
  if(is_sign_in.value){
    axios.post('http://localhost:8081/'+Userinfo.value.userid+'/upload',fleet_list,
  {
    headers: {
      'Content-Type': 'application/json', // 请求头
      // 其他请求头配置
    },
    responseType: 'json' // 响应类型
    // 其他配置选项
  }).then(
    console.log("upload success")
  ).catch(error=>{
      window.alert("無法更新資料："+error.toString());
      console.log(error);
    })
  }
})

//程式內函式
const add_fleet = () => {
  if (fleetname.value.trim() !== '') {
    fleet_list.push({
      name:fleetname.value,
      imgurl:["remove","remove","remove","remove","remove","remove"]
    });
    fleetname.value = '';
  }
};

const remove_fleet = (index) => {
  fleet_list.splice(index,1);
};

const getButtom_style = (button_id, fleet_id) => {
  return require(`@/assets/shipicon/${fleet_list[fleet_id].imgurl[button_id]}.png`);
};

const chosen_character = (item) => {
  fleet_list[chosen_fleet_index.value].imgurl[chosen_buttonid.value] = item.shipname;
  close_ship_list();
}

const close_ship_list = ()=>{
    show_shiplist.value=false;
}
const open_ship_list = (button_id,fleet_id)=>{
  show_shiplist.value=true;
  chosen_buttonid.value=button_id;
  chosen_fleet_index.value=fleet_id;
}

const ship_data=reactive([])

const getpic = () => {
  const requireContext = require.context('@/assets/shipicon', true, /\.(png|jpe?g|svg)$/);
  const paths = requireContext.keys();
  paths.forEach((path) => {
    ship_data.push({shipname: getname(path)});
    
  });
};

const getname=(path)=>{
    const temp=path.split("/");
    return temp[temp.length-1].split(".")[0];
}
onMounted(() => {
  getpic();
});

</script>

<style scoped>
.scroll-container {
  overflow: hidden; /* 隐藏滚动条 */
}
.fade-enter-active, .fade-leave-active {
  transition: opacity 0.1s; /* 过渡属性和持续时间 */
}
.fade-enter, .fade-leave-to /* .fade-leave-active 在 Vue 2.1.8+ 中可使用 */ {
  opacity: 0; /* 开始状态和结束状态 */
}
.memo-form {
  margin-bottom: 10px;
}

ul {
  list-style: none;
  padding: 0;
}

li {
  display: flex;
  justify-content: space-around;
  align-items: center;
  margin-bottom: 5px;
}

#popup_shiplist {
    position: absolute;
    top: 10px;
    left: 50px;
    backdrop-filter:blur(8px);
    padding: 20px;
    box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.5);
    transition: opacity 1s;
  }
#popup_login{
    display: flex;
    flex-direction: column;
    position: absolute;
    top: 50%;
    left: 50%;
    backdrop-filter:blur(8px);
    padding: 20px;
    box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.5);
}
.ship{
  width: 100px;
  height: 100px;
  margin: 5px;
  border:none;
  background-color: transparent;

}
#shipgrid{
  display: flex;
  flex-wrap: wrap;
  width: 400px;
}
#shipsort{
      display: flex;
      flex-wrap: wrap;
      
}
.shipitem {
    width: 100px; /* 计算每个项目的宽度，减去一些间距 */
    height: 150px;
    margin: 10px;
}
#fliter{
    display: flex;
    justify-content: space-between;
    }

#titlebar{
  display: flex;
  justify-content: space-between;
  background-color: bisque;
}

#close_ship_list{
  position: fixed;
  bottom:20px;
  right:20px;
  z-index: 1;
  background-color: red;
  backdrop-filter: blur(10px);
  padding: 30px;
  border-radius: 200px;
  border:none;


}
</style>