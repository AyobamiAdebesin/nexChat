<template>
  <div id="app">
    <LoginUser />
    <b-container>
      <NavBar :logged_user="logged_user_username" />
      <b-row class="main-area">
        <b-col cols="4" class="users">
          <UserList />
        </b-col>
        <b-col cols="8" class="messages-area">
          <div class="messages-main">
            <div 
              v-if="!current_chat_channel" 
              class="select-chat text-center"
            >
              Select a user to start chatting... 
            </div>
            <ChatMessage
              v-else 
              :active_chat="active_chat_id" 
              :messages="messages[current_chat_channel]"
            /> 
          </div>
          <MessageInput />
        </b-col>
      </b-row>
    </b-container>
  </div>
</template>

<script>
import MessageInput from './components/MessagesInput.vue';
import ChatMessage from './components/ChatMessage.vue';
import NavBar from './components/NavBar.vue';
import LoginUser from './components/LoginUser.vue';
import UserList from './components/UserList.vue';

// declare pusher variable



export default {
  name: 'App',
  components: {
    MessageInput,
    NavBar,
    ChatMessage,
    UserList,
    LoginUser,
  },
  data: function () {},
  methods: {},

};
</script>

<style lang="scss">
@import "~@/assets/scss/vendors/bootstrap-vue/index";
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
.messages-main {
  overflow-y: scroll;
  height: 90%;
}
.users {
  padding: 0px !important;
  border: 1px solid gray;
}
.no-margin {
  margin: 0px;
}
.messages-area {
  border: 1px solid gray;
  padding: 0px !important;
  max-height: calc(100vh - 4em) !important;
}
.input-message {
  height: 40px;
}
.active {
  background: #17a2b8 !important;
  border: #17a2b8 !important;
}
.select-chat {
  margin-top: 35vh;
  padding: 8px;
}
.main-area {
  margin: 0px;
  min-height: calc(100vh - 5em) !important;
}
.logged_user {
  color: white;
}
</style>
