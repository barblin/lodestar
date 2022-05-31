import {createRouter, createWebHistory} from "vue-router";
import Dashboard from "./components/Dashboard.vue";
import ResourceManager from "./components/ResourceManager.vue";
import Tutorial from "./components/Tutorial.vue";

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
    {
        path: "/tutorial",
        name: "Tutorial",
        component: Tutorial,
    },
];

const router = createRouter({
    history: createWebHistory(),
    routes,
});

export default router;