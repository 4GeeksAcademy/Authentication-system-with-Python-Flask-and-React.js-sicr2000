const getState = ({ getStore, getActions, setStore }) => {
  return {
    store: {
      message: null,
      token: localStorage.getItem("token") || null,
      profile: null,
    },
    actions: {
      // Use getActions to call a function within a fuction
      exampleFunction: () => {
        getActions().changeColor(0, "green");
      },

      getMessage: async () => {
        try {
          // fetching data from the backend
          const resp = await fetch(process.env.BACKEND_URL + "/api/hello");
          const data = await resp.json();
          setStore({ message: data.message });
          // don't forget to return something, that is how the async resolves
          return data;
        } catch (error) {
          console.log("Error loading message from backend", error);
        }
      },
      register: async (newUser) => {
        try {
          const resp = await fetch(
            process.env.BACKEND_URL + "/api/accounts/user",
            {
              method: "POST",
              headers: {
                "Content-Type": "application/json",
              },
              body: JSON.stringify(newUser),
            }
          );
          const data = await resp.json();

          setStore({ profile: data.newUser, token: data.token });
          localStorage.setItem("token", data.token);

          return true;
        } catch (error) {
          console.log("Error loading message from backend", error);
          return false;
        }
      },
      login: async (email, password) => {
        
        try {
          const resp = await fetch(process.env.BACKEND_URL + "/api/token", {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify({ email, password }),
          });
          const data = await resp.json();
          localStorage.setItem("token", data.token); //guardar token en localstorage
          setStore({ profile: null, token: data.token });
          getActions().getProfile();
          return true;
        } catch (error) {
          console.log("Error loading message from backend", error);
          return false;
        }
      },
      getProfile: async () => {
        let store = getStore();

        if (store.profile && !store.profile.msg) return;
        try {
          const resp = await fetch(process.env.BACKEND_URL + "/api/profile", {
            method: "GET",
            headers: {
              "Content-Type": "application/json",
              Authorization: "Bearer " + store.token,
            },
          });
          if (resp.status == 401 || resp.status == 422) {
            localStorage.removeItem("token")
            setStore({ profile: null, token: null });
            return console.log(store);
          }
          const data = await resp.json();
          setStore({ profile: data, token: store.token });
        } catch (error) {
          console.log("Error loading message from backend", error);
        }
      },
      logOut: () => {
        localStorage.removeItem("token"); //elimanaria el token
        setStore({ token: null, profile: null });
      },
    },
  };
};

export default getState;
