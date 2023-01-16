<script>
import store from './store';

export default {
    name: 'App',
    computed: {
        messages: () => store.getters.get_messages
    },
}
</script>

<template>
    <Message class="position-absolute" style="left: 15%; right: 15%"  v-for="msg of messages" :severity="msg.severity" :key="msg.content"
           :closable="msg.closable" :icon="msg.icon" :sticky="false">{{ msg.content }}</Message>
    <router-view />
</template>

<style scoped></style>
