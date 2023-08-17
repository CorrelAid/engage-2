module.exports = {
  root: true,
  env: {
    node: true,
  },
  extends: [
    "plugin:vue/vue3-essential",
    "eslint:recommended",
    "@vue/eslint-config-typescript",
    "plugin:prettier/recommended",
  ],
  rules: {
    "vue/multi-word-component-names": "off",
    "no-unused-vars": "error",
  },
};
