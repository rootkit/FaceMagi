<template>
	<view class="uni-steps">
		<view class="uni-steps-items" :class="'uni-steps-' + direction">
			<view class="uni-steps-item" v-for="(item,index) in steps" :key="index" :class="[item.status ? 'uni-steps-' + item.status : '']">
				<view class="uni-steps-item-title-container" :style="{color:item.status === 'process' ? activeColor : ''}">
					<view class="uni-steps-item-title">{{ item.title }}</view>
					<view class="uni-steps-item-desc" v-if="item.desc">{{ item.desc}}</view>
				</view>
				<view class="uni-steps-item-circle-container">
					<view class="uni-steps-item-circle" v-if="item.status !== 'process'" :style="{backgroundColor:item.status === 'finish' ? activeColor : ''}"></view>
					<uni-icon v-else type="checkbox-filled" size="14" :color="activeColor"></uni-icon>
				</view>
				<view class="uni-steps-item-line" v-if="index !== steps.length-1" :style="{backgroundColor:item.status === 'finish' ? activeColor : ''}"></view>
			</view>
		</view>
	</view>
</template>

<script>
	import uniIcon from '../ts-icon/ts-icon.vue'
	export default {
		name: "ts-steps",
		components: {
			uniIcon
		},
		props: {
			direction: { //排列方向 row column
				type: String,
				default: 'row'
			},
			activeColor: { //激活状态颜色
				type: String,
				default: '#1aad19'
			},
			active: { //当前步骤
				type: [Number, String],
				default: 0
			},
			data: Array //数据
		},
		data() {
			return {}
		},
		computed: {
			steps() {
				let steps = []
				this.data.forEach((item, index) => {
					let step = {}
					step.title = item.title
					step.desc = item.desc
					step.status = this.getStatus(index)
					steps.push(step)
				})
				return steps
			}
		},
		methods: {
			getStatus(index) {
				if (index < Number(this.active)) {
					return 'finish'
				} else if (index === Number(this.active)) {
					return 'process'
				}
				return ''
			}
		}
	}
</script>

<style lang="scss">
    $uni-border-color-light:#ebedf0;//较浅的灰色，如steps时间轴的颜色
	.uni-steps {
		width: 100%;
		box-sizing: border-box;
		display: flex;
		flex-direction: column;
		overflow: hidden;
		position: relative;

		&-items {
			position: relative;
			display: flex;
			flex-direction: row;
			margin: 10px;
			box-sizing: border-box;
			overflow: hidden;

			&.uni-steps-column {
				margin: 10px 0;
				padding-left: 31px;
				flex-direction: column;

				.uni-steps-item {
					&:after {
						content: ' ';
						position: absolute;
						height: 1px;
						width: 100%;
						bottom: 9px;
						left: 0;
						background-color: $uni-border-color-light;
						transform: scaleY(0.5);
					}

					&:last-child {
						position: relative;

						&:after {
							height: 0px;
						}

						.uni-steps-item-title-container {
							text-align: left;
						}

						.uni-steps-item-circle-container {
							left: -17px;
							right: auto
						}
					}

					&-title-container {
						transform: none;
						display: block;
						line-height: 36upx;
					}

					&-title {
                        text-overflow: ellipsis;
                        white-space: nowrap;
                        overflow: hidden;
                    }

					&-desc {
						white-space: normal;
						display: -webkit-box;
						-webkit-box-orient: vertical;
						-webkit-line-clamp: 2;
						overflow: hidden;
					}

					&-circle-container {
						left: -17px;
						top: -1px;
						bottom: auto;
						padding: 8px 0px;
						z-index: 1;
					}

					&-line {
						height: 100%;
						width: 1px;
						left: -15px;
						top: -1px;
						bottom: auto;
					}


					&.uni-steps-process {
						.uni-steps-item-circle-container {
							bottom: auto;
							left: -21px;
						}
					}
				}
			}
		}

		&-item {
			flex: 1;
			position: relative;
			padding-bottom: 18px;

			&-title-container {
				text-align: left;
				margin-left: 3px;
				display: inline-block;
				transform: translateX(-50%);
				color: $uni-text-color-grey;
			}

			&-title {
				font-size: $uni-font-size-base;
			}

			&-desc {
				font-size: $uni-font-size-sm;
			}

			&:first-child {
				.uni-steps-item-title-container {
					transform: none;
					margin-left: 0;
				}
			}

			&:last-child {
				position: absolute;
				right: 0;

				.uni-steps-item-title-container {
					transform: none;
					text-align: right;
				}

				.uni-steps-item-circle-container {
					left: auto;
					right: -8px
				}
			}

			&-circle-container {
				position: absolute;
				bottom: 8px;
				left: -8px;
				padding: 0 8px;
				background-color: $uni-bg-color;
				z-index: 1;
			}

			&-circle {
				width: 5px;
				height: 5px;
				background-color: $uni-text-color-grey;
				border-radius: $uni-border-radius-circle;
			}

			&-line {
				background-color: $uni-border-color-light;
				position: absolute;
				bottom: 10px;
				left: 0;
				width: 100%;
				height: 1px;
			}

			&.uni-steps-finish {
				.uni-steps-item-title-container {
					color: $uni-text-color;
				}
			}

			&.uni-steps-process {
				.uni-steps-item-circle-container {
					bottom: 3px;
					display: flex;
				}
			}
		}
	}
</style>
