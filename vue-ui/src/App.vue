<template>
  <div id="app" class="container">
    <div v-if="loading" class="loading">
      Loading...
    </div>
    <div class="row">
      <div class="col-12 col-md-6 col-lg-4" v-for="s in servers" :key="s.name">
        <Server :data="s" />
      </div>
    </div>
  </div>
</template>

<script>
import Server from "./components/Server.vue";
import api from "./api";

export default {
  name: "App",
  components: {
    Server
  },
  data: () => ({
    loading: false,
    servers: []
  }),
  created() {
    this.loading = true;
    api.getServers().then(result => {
      this.servers = result;
      this.loading = false;
    });
  }
};
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
  opacity: .6;
}
</style>
