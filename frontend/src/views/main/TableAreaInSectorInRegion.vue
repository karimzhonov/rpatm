<template>
<BackOrStart/>
  <div class="row">
    <div class="col">
      <div>
        <DataTable :value="items" showGridlines responsiveLayout="scroll">
          <template #header>
            <p class="text-center">Демография</p>
          </template>
          <Column field="maxalla" header="Махалла"></Column>
          <Column field="name" header="Аҳоли сони"></Column>
          <Column field="category" header="Ер майдони (кв.м)"></Column>
          <Column field="quantity" header="Аҳоли зичлиги (хар 1000 кв. м.га)"></Column>
          <Column field="quantity" header="Аёллар сони"></Column>
          <Column field="quantity" header="Эркаклар сони"></Column>
          <Column field="quantity" header="Оила сони"></Column>
          <Column field="quantity" header="Ахолининг ўртача ёши"></Column>
        </DataTable>
      </div>
    </div>
  </div>
</template>

<script>
import BackOrStart from "@/components/BackOrStart.vue";

export default {
  name: "TableAreaInSectorInRegion",
  props: ['id', 'table_id'],
  data() {
    return {
      items: [
        {
          maxalla: 'Алишер Навоий',
        },
        {
          maxalla: 'Ийк ота',
        },
        {
          maxalla: 'Мажнунтол'
        }
      ]
    }
  },
  components: {BackOrStart}
}
</script>

<style scoped>

</style>