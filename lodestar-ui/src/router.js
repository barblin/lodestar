import { createWebHistory, createRouter } from "vue-router";
import Dashboard from "./components/Dashboard.vue";
import ResourceManager from "./components/ResourceManager.vue";

const routes = [
    {
        path: "/",
        name: "Input",
        component: Dashboard,
    },
    {
        path: "/resources",
        name: "ResourceManager",
        component: ResourceManager,
    },
];

const router = createRouter({
    history: createWebHistory(),
    routes,
});

export default router;