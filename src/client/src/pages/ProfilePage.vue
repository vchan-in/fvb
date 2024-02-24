<template>
  <div class="profile-page">
    <h1>User Profile</h1>
    <div class="user-info">
      <div class="avatar">
        <img :src="user.avatar" alt="User Avatar" />
      </div>
      <div class="details">
        <h2>{{ user.name }}</h2>
        <p>Email: {{ user.email }}</p>
        <p>Location: {{ user.location }}</p>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      user: {
        name: "John Doe",
        email: "johndoe@example.com",
        location: "New York, USA",
        avatar: "https://example.com/avatar.jpg",
      },
    };
  },
};
</script>

<style scoped>
.profile-page {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

.user-info {
  display: flex;
  align-items: center;
}

.avatar {
  width: 100px;
  height: 100px;
  border-radius: 50%;
  overflow: hidden;
  margin-right: 20px;
}

.avatar img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.details {
  flex: 1;
}

h1 {
  font-size: 24px;
  margin-bottom: 10px;
}

h2 {
  font-size: 20px;
  margin-bottom: 5px;
}

p {
  margin-bottom: 5px;
}
</style>
