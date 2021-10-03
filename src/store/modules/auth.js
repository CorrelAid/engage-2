const state = {
  user: null,
  accessToken: null,
};

const getters = {
  accessToken: (state) => state.accessToken,
  isAuthenticated: (state) => !!state.accessToken,
};

const mutations = {
  commitUser: (state, user) => (state.user = user),
  commitAccessToken: (state, accessToken) => (state.accessToken = accessToken),
};

const actions = {
  setUser: (context, user) => context.commit("commitUser", user),
  setToken: (context, token) => {
    context.commit("commitAccessToken", token.access_token);
  },
};

export default {
  namespaced: true,
  state,
  getters,
  mutations,
  actions,
};
