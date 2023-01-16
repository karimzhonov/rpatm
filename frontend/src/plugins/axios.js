import axios from "axios";
import store from "@/store";
import router from "@/router";
import { computed } from "vue";

const $api = axios.create({
    baseURL: process.env.VUE_APP_BACKEND_HOST,
});

export default {
    $api,
    async raise_error_400(data) {
        if (data.detail) {
            for (let message of data.detail) {
                await store.dispatch('add_error_message', message)
            }
        }
        delete data.detail
        for (let key in data) {
            document.getElementById(`${key}_error`).innerText = data[key].join('. ')
        }
    },
    async raise_error(response) {
        if (response.status === 401) {
            if (localStorage.getItem('refresh')) {
                await store.dispatch('refresh_token', localStorage.getItem('refresh'))
                return
            }
            await router.push({name: 'login'})
        } else if (response.status === 400) {
            await this.raise_error_400(response.data)
        }
        throw response.data
    },
    async delete_errors(){
        for (let element of document.querySelectorAll('[id$=_error]')) {
            element.innerText = ''
        }
    },
    async get_headers() {
        this.delete_errors()
        const headers = {}
        headers['Accept-Language'] = localStorage.getItem('lang') ?? 'ru'
        if (localStorage.getItem('access')) {
            headers['Authorization'] = `Bearer ${localStorage.getItem('access')}`
        }
        headers['Accept-Language'] = localStorage.getItem('lang')
        return headers
    },
    async get(url, options = {}) {
        options.headers = await this.get_headers();
        try {
            return await $api.get(url, options);
        } catch (e) {
            await this.raise_error(e.response);
            return await this.get(url, options)
        }
    },
    async post(url, data, options = {}) {
        options.headers = await this.get_headers();
        try {
            return await $api.post(url, data, options);
        } catch (e) {
            await this.raise_error(e.response);
            return await this.post(url, data, options)
        }
    },
    async patch(url, data, options = {}) {
        options.headers = await this.get_headers();
        try {
            return await $api.patch(url, data, options);
        } catch (e) {
            await this.raise_error(e.response);
            return await this.patch(url, data, options)
        }
    },
    async delete(url, options = {}) {
        options.headers = await this.get_headers();
        try {
            return await $api.delete(url, options);
        } catch (e) {
            await this.raise_error(e.response);
            return await this.delete(url, options)
        }
    },
    async head(url, options = {}) {
        options.headers = await this.get_headers();
        try {
            return await $api.head(url, options);
        } catch (e) {
            await this.raise_error(e.response);
        }
    },
};
