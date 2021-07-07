<template>
  <div class="card mb-2">
    <div class="card-body">
      <h5 class="card-title">
        {{ data.name }} <small class="text-muted">(:{{ data.port }})</small>
      </h5>
      <h6 class="card-subtitle mb-2">
        {{ data.description }}
        <sup :class="$style.toggleMods" @click="toggleMods">
          {{ showMods ? "Hide Mods" : "View Mods" }}
        </sup>
      </h6>
      <transition name="curtain">
        <div :class="[$style.mods, 'card-body']" v-if="showMods">
          <ul class="list-group">
            <li
              class="list-group-item d-flex w-100 justify-content-between align-items-center"
              v-for="m in data.mods"
              :key="m"
            >
              <span>{{ m }}</span>
              <button class="btn" @click="onRemoveMod(m)" :disabled="loading">
                <TrashIcon />
              </button>
            </li>
            <li
              v-if="data.mods.length == 0"
              class="list-group-item text-warning"
            >
              No mod found!
            </li>
            <li class="list-group-item border-0">
              <input
                type="file"
                class="d-none"
                @change="onAddMod"
                accept=".JAR"
                ref="filePicker"
              />
              <button class="btn btn-success" @click="$refs.filePicker.click()">
                <PlusIcon />
                Add Mod
              </button>
            </li>
          </ul>
        </div>
      </transition>
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
          class="btn btn-primary"
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
          <PlayIcon v-if="!loading" />
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
          <StopIcon v-if="!loading" />
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
import TrashIcon from "bootstrap-icons/icons/trash.svg";
import PlusIcon from "bootstrap-icons/icons/plus.svg";
import PlayIcon from "bootstrap-icons/icons/play-fill.svg";
import StopIcon from "bootstrap-icons/icons/stop-fill.svg";

export default {
  name: "Server",
  components: {
    TrashIcon,
    PlusIcon,
    PlayIcon,
    StopIcon
  },
  data: () => ({
    loading: false,
    message: null,
    error: null,
    showMods: false,
    showModUpload: true
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
    toggleMods() {
      this.showMods = !this.showMods;
    },
    onRemoveMod(mod) {
      if (confirm("Remove mod " + mod + "?")) {
        this.loading = true;
        api.removeMod(this.data.name, mod).then(
          s => {
            Object.assign(this.data, s);
            this.message = "Mod removed (remember to restart the server!)";
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
    },
    onAddMod(e) {
      if (e.target.files && e.target.files.length) {
        this.loading = true;
        api.addMod(this.data.name, e.target.files[0]).then(
          s => {
            Object.assign(this.data, s);
            this.message = "Mod added (remember to restart the server!)";
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

<style module lang="scss">
.toggleMods {
  color: blue;
  cursor: pointer;
}
.mods {
  li {
  }
}
</style>
