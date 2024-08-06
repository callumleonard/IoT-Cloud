#include <linux/kernel.h>
#include <linux/module.h>
#include <linux/init.h>
#include <linux/fs.h>
#include <linux/device.h>
#include <linux/gpio.h>

MODULE_LICENSE("GPL");
MODULE_AUTHOR("CallumL - 1902922");
MODULE_DESCRIPTION("Mem-map - GPIO device driver for pulling HIGH/LOW LED");
MODULE_VERSION("0.3");

#define DEVICE_NAME "lkm01"
#define MAJOR_NUM 42
#define PIN_NUM  25

#define BCM2708_PERI_BASE       0x20000000
#define GPIO_BASE               (BCM2708_PERI_BASE + 0x200000)	// GPIO controller

/* macros -  use INP_GPIO(x) before using OUT_GPIO(x) */
#define INP_GPIO(g)   *(gpio.addr + ((g)/10)) &= ~(7<<(((g)%10)*3))
#define OUT_GPIO(g)   *(gpio.addr + ((g)/10)) |=  (1<<(((g)%10)*3))
#define SET_GPIO_ALT(g,a) *(gpio.addr + (((g)/10))) |= (((a)<=3?(a) + 4:(a)==4?3:2)<<(((g)%10)*3))
#define GPIO_SET  *(gpio.addr + 7)
#define GPIO_CLR  *(gpio.addr + 10)

#define GPIO_READ(g)  *(gpio.addr + 13) &= (1<<(g))

struct bcm2835_peripheral {
    unsigned long addr_p;
    int mem_fd;
    void *map;
    volatile unsigned int *addr;
};

struct bcm2835_peripheral gpio = {GPIO_BASE};

static int lkm01_open(struct inode *inode, struct file *file){
    pr_info("CMP408: %s\n", __func__);
    return 0;
}
static int lkm01_release(struct inode *inode, struct file *file){
    pr_info("CMP408: %s\n", __func__);
    return 0;
}
static ssize_t lkm01_read(struct file *file,
            char *buffer, size_t length, loff_t * offset){
    pr_info("CMP408: %s %u\n", __func__, length);
    return 0;
}
static ssize_t lkm01_write(struct file *file,
             const char *buffer, size_t length, loff_t * offset){
    pr_info("CMP408: %s %u\n", __func__, length);
    return length;
}
struct file_operations lkm01_fops = {
    .owner = THIS_MODULE,
    .open = lkm01_open,
    .release = lkm01_release,
    .read = lkm01_read,
    .write = lkm01_write,
};
int __init lkm01_init(void){
    int ret;
    pr_info("CMP408: %s\n", __func__);

    ret = register_chrdev(MAJOR_NUM, DEVICE_NAME, &lkm01_fops);
    if (ret != 0)
        return ret;

        gpio.map     = ioremap(GPIO_BASE, 4096);
    	gpio.addr    = (volatile unsigned int *)gpio.map;

    	INP_GPIO(PIN_NUM);
    	OUT_GPIO(PIN_NUM);
    	GPIO_SET = 1 << PIN_NUM;

    printk("CMP408: lkm01 loaded\n");
    return 0;
}
void __exit lkm01_exit(void){
    unregister_chrdev(MAJOR_NUM, DEVICE_NAME);
    GPIO_CLR = 1 << PIN_NUM;
    if (gpio.addr){

            iounmap(gpio.addr);
    	}

    printk("CMP408: lkm01 unloaded\n");
}
module_init(lkm01_init);
module_exit(lkm01_exit);