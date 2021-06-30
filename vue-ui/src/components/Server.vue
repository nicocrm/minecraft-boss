<template>
  <div class="card mb-2">
    <div class="card-body">
      <h5 class="card-title">{{ data.name }}</h5>
      <h6 class="card-subtitle mb-2">{{ data.description }}</h6>
      <div class="card-text">Server port: {{ data.port }}</div>
      <div class="card-text">
        Server status:
        <span
          :class="{
            'text-danger': !data.is_running,
            'text-success': data.is_running
          }"
          >{{ data.is_running ? "RUNNING" : "NOT RUNNING" }}</span
        >
      </div>
      <div class="m-4">
        <button
          class="btn btn-success"
          @click="onStart"
          :disabled="loading"
          v-if="!data.is_running"
        >
          <span
            class="spinner-border spinner-border-sm"
            role="status"
            aria-hidden="true"
            v-if="loading"
          ></span>
          <span class="visually-hidden" v-if="loading">Loading...</span>
          Start
        </button>
        <button
          class="btn btn-danger"
          @click="onStop"
          :disabled="loading"
          v-if="data.is_running"
        >
          <span
            class="spinner-border spinner-border-sm"
            role="status"
            aria-hidden="true"
            v-if="loading"
          ></span>
          <span class="visually-hidden" v-if="loading">Loading...</span>
          Stop
        </button>
      </div>
      <div class="alert alert-success" v-if="message">
        {{ message }}
      </div>
      <div class="alert alert-danger" v-if="error">
        There was an error: {{ error }}
      </div>
    </div>
  </div>
</template>

<script>
import api from "../api";

export default {
  name: "Server",
  components: {},
  data: () => ({
    loading: false,
    message: null,
    error: null
  }),
  props: {
    data: Object
  },
  methods: {
    onStart(e) {
      e.preventDefault();
      this._controlServer("start");
    },
    onStop(e) {
      e.preventDefault();
      this._controlServer("stop");
    },
    _controlServer(operation) {
      this.loading = true;
      api.controlServer(this.data.name, operation).then(
        s => {
          Object.assign(this.data, s);
          this.message = "Request sent";
          this.error = null;
          this.loading = false;
        },
        err => {
          this.message = null;
          this.error = String(err);
          this.loading = false;
        }
      );
    }
  }
};
</script>
