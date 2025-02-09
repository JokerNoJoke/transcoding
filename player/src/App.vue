<script setup lang="ts">
import videojs from "video.js";
import "video.js/dist/video-js.min.css";
import "videojs-contrib-quality-menu";
import type Player from "video.js/dist/types/player";
import { onMounted, onUnmounted, ref } from "vue";

const inputRef = ref<HTMLInputElement | null>(null);

const uploadFile = async () => {
  const fileInput = inputRef.value;
  if (!fileInput || !fileInput.files || fileInput.files.length === 0) {
    return;
  }

  const formData = new FormData();
  formData.append("file", fileInput.files[0]);

  try {
    const response = await fetch("http://127.0.0.1:8000/os/mp4", {
      method: "POST",
      body: formData,
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json();
    console.log("Upload successful:", data);

    if (player) {
      player.ready(function () {
        player.src(
          `http://127.0.0.1:9000/minio-transcoding/${data.manifest_url}`
        );
      });
    }
  } catch (error) {
    console.error("Error uploading file:", error);
  }
};

const options = {
  controls: true,
  preload: "metadata",
};

let player: Player;

onMounted(() => {
  player = videojs("vid", options, function () {
    // this.log("onPlayerReady", this);
    this.qualityLevels();
    this.qualityMenu();
    this.src(
      "http://127.0.0.1:9000/minio-transcoding/videos/dash/manifest.mpd"
    );
  });
});

onUnmounted(() => {
  player.dispose();
});
</script>

<template>
  <div class="h-screen flex flex-col justify-center items-center">
    <div class="mb-4">
      <input ref="inputRef" accept="video/*" type="file" />
      <button @click="uploadFile">Upload Video</button>
    </div>
    <video class="video-js" id="vid"></video>
  </div>
</template>

<style scoped>
.mb-4 {
  margin-bottom: 1rem;
}
.h-screen {
  height: 100vh;
}
.flex {
  display: flex;
}
.flex-col {
  flex-direction: column;
}
.justify-center {
  justify-content: center;
}
.items-center {
  align-items: center;
}
</style>
