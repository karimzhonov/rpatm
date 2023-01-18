<template>
  <div class="flex justify-content-between align-items-center mb-4">
    <div>
<!--      <Button icon="pi pi-arrow-circle-left" @click="go_back"/>-->
      <Breadcrumb :model="navigator" :home="home" class="rounded-3"/>
    </div>
    <h1 class="m-0">
      {{ header }}
    </h1>
    <div>
      <router-link :to="{name: 'home'}">
        <Button :label="$t('Перейти на главную страницу')"/>
      </router-link>
    </div>
  </div>
</template>

<script>
export default {
  name: "BackOrStart",
  props: ['header', 'navigator'],
  data() {
    return {
      home: {icon: 'pi pi-home', to: {name: 'ichd_main', query: this.$route.query}},
    }
  },
  methods: {
    go_back() {
      window.history.back()
    }
  }
}
</script>

<style scoped>

</style>