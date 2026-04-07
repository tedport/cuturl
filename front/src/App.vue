<script setup>
import LinkCreate from './components/LinkCreate.vue';
import Management from './components/Management.vue';

</script>

<template>
	<div class="min-vh-100 bg-light pt-4">
		<div class="container">
			<div class="row justify-content-center g-1">
				<div class="col-12 col-md-6 col-xl-5">
					<LinkCreate />
				</div>
				<div class="col-12 col-md-6 col-xl-5">
					<Management />
				</div>
			</div>
		</div>
	</div>
</template>

<style scoped>
div {
	padding-bottom: 75%;
}
</style>
