import tensorflow as tf
from tensorflow import keras
from keras import layers
from keras.models import Sequential
import matplotlib.pyplot as plt


class mANregression(keras.Model):
    def __init__(self,ninputs):
        super(mANregression,self).__init__()
        self.discriminator = self.build_discriminator(1)
        self.generator     = self.build_generator(ninputs)

    def build_discriminator(self,ninput):
        dis_input = layers.Input((ninput,))
        label_input = layers.Input((1,))
        merge_input = keras.layers.Concatenate()([dis_input,label_input])

        layer = layers.Dense(400,activation ='relu', kernel_initializer='he_uniform')(merge_input)
        layer = layers.Dense(100,activation ='relu', kernel_initializer='he_uniform')(layer)
        out_layer = layers.Dense(1,activation='sigmoid')(layer)
        model = tf.keras.Model(merge_input,out_layer)
        return model

    def build_generator(self,input_dim):
        model = Sequential()
        model.add(keras.layers.Flatten(input_shape=input_dim))
        hlayer_outline = {'hlayer1':200,'hlayer2':400,'hlayer4':200}
        for layer in hlayer_outline:
            model.add(keras.layers.Dense(hlayer_outline[layer],activation='relu'))
            #model.add(LeakyReLU(alpha=0.1))
        model.add(keras.layers.Dense(1,activation='linear'))
        return model

    def compile(self, d_optimizer, g_optimizer, loss_fn, gen_loss_fn, d_loss_weight, g_loss_weight):
        super(mANregression, self).compile()
        self.d_optimizer = d_optimizer
        self.g_optimizer = g_optimizer
        self.loss_fn = loss_fn
        self.d_loss_metric = keras.metrics.Mean(name="d_loss")
        self.g_loss_metric = keras.metrics.Mean(name="g_loss")
        self.gen_loss_fn = gen_loss_fn
        self.d_loss_weight = d_loss_weight
        self.g_loss_weight = g_loss_weight

    def train_step(self,data):
        dnn_train,real_vis_mass= data
        batch_size = tf.shape(dnn_train)[0]

        in_features = dnn_train #tf.random.normal(shape=(batch_size,1),mean=0.0)
        generated_vis_mass = self.generator(dnn_train)

        fake_vismass_labels = tf.concat([generated_vis_mass,in_features],-1)
        real_vismass_labels = tf.concat([real_vis_mass,in_features],-1)

        combined_variable = tf.concat([fake_vismass_labels,real_vismass_labels],axis=0)
        labels = tf.concat(
            [tf.ones((batch_size,1)), tf.zeros((batch_size,1))], axis=0
        )
        with tf.GradientTape() as tape:
             predictions = self.discriminator(combined_variable)
             d_loss = self.d_loss_weight * self.loss_fn(labels, predictions)
        grads = tape.gradient(d_loss, self.discriminator.trainable_weights)
        self.d_optimizer.apply_gradients(
            zip(grads, self.discriminator.trainable_weights)
        )

        # Assemble labels that say "all real images"
        misleading_labels = tf.zeros((batch_size, 1))

        # Train the generator (note that we should *not* update the weights
        # of the discriminator)!
        with tf.GradientTape() as tape:
          generated_vis_mass = self.generator(dnn_train)
          fake_vismass_labels = tf.concat([generated_vis_mass,in_features],-1)
          predictions = self.discriminator(fake_vismass_labels)
          g_loss_1 =self.g_loss_weight *  self.loss_fn(misleading_labels, predictions)
          g_loss_2 =self.g_loss_weight *  self.gen_loss_fn(real_vis_mass,generated_vis_mass)
          g_loss = g_loss_1 + g_loss_2

        #grads_gen = tape.gradient(gen_loss, self.generator.trainable_weights)
        grads = tape.gradient(g_loss, self.generator.trainable_weights)
        #grads_tot = grads + grads_gen
        self.g_optimizer.apply_gradients(zip(grads, self.generator.trainable_weights))
        # Update metrics
        self.d_loss_metric.update_state(d_loss)
        self.g_loss_metric.update_state(g_loss)
        return {
            "d_loss": self.d_loss_metric.result(),
            "g_loss": self.g_loss_metric.result(),
            "g_loss_loss": g_loss_1,
        }

class mANMonitor(keras.callbacks.Callback):
    def __init__(self,real_tau_p4,vis_mass,prefix,incriment):
        self.real_tau_p4 = real_tau_p4
        self.incriment = incriment
        self.prefix = prefix
        self.vis_mass = vis_mass



    def summarise_performance(self,real_boson_mass,fake_boson_mass):
        fig,ax = plt.subplots()
        (n1, bins1, patches1)=ax.hist(real_boson_mass,20,color='blue',label='real')
        (n2, bins2, patches2)=ax.hist(fake_boson_mass,20,color='red',alpha=0.5,label='fake')
        #ax.scatter(real_tau_p4[:,0],real_tau_p4[:,1],color='blue',label='real')
        #ax.scatter(fake_tau_p4[:,0],fake_tau_p4[:,1],color='red',label='fake')

        ax.legend()


    def SaveModels(self,epoch):
        discriminator = self.model.discriminator
        generator = self.model.generator
        discriminator.trainable = False
        tf.keras.models.save_model(generator,'/content/drive/MyDrive/GAN_Regression/generator_'+self.prefix+'_'+str(epoch))
        tf.keras.models.save_model(discriminator,'/content/drive/MyDrive/GAN_Regression/discriminator_'+self.prefix+'_'+str(epoch))

    def on_epoch_end(self, epoch, logs=None):

        generated_vismass_labels = self.real_tau_p4
        self.fake_vismass  = self.model.generator(generated_vismass_labels)
        if epoch % self.incriment == 0 and epoch != 0:
          self.summarise_performance(self.vis_mass,self.fake_vismass[:,0])
          self.SaveModels(epoch)

class LoadmANregression(keras.Model):
    def __init__(self,generator,discriminator,ninputs):
        super(LoadmANregression,self).__init__()
        self.discriminator = discriminator
        self.generator     = generator

    def compile(self, d_optimizer, g_optimizer, loss_fn, gen_loss_fn, d_loss_weight, g_loss_weight):
        super(LoadmANregression, self).compile()
        self.d_optimizer = d_optimizer
        self.g_optimizer = g_optimizer
        self.loss_fn = loss_fn
        self.d_loss_metric = keras.metrics.Mean(name="d_loss")
        self.g_loss_metric = keras.metrics.Mean(name="g_loss")
        self.gen_loss_fn = gen_loss_fn
        self.d_loss_weight = d_loss_weight
        self.g_loss_weight = g_loss_weight

    def train_step(self,data):
        dnn_train,real_vis_mass= data
        batch_size = tf.shape(dnn_train)[0]

        fake_labels = dnn_train#tf.random.normal(shape=(batch_size,1),mean=0.0)
        generated_vis_mass = self.generator(dnn_train)

        fake_vismass_labels = tf.concat([generated_vis_mass,fake_labels],-1)
        real_vismass_labels = tf.concat([real_vis_mass,fake_labels],-1)

        combined_variable = tf.concat([fake_vismass_labels,real_vismass_labels],axis=0)
        labels = tf.concat(
            [tf.ones((batch_size,1)), tf.zeros((batch_size,1))], axis=0
        )
        with tf.GradientTape() as tape:
             predictions = self.discriminator(combined_variable)
             d_loss = self.d_loss_weight * self.loss_fn(labels, predictions)
        grads = tape.gradient(d_loss, self.discriminator.trainable_weights)
        self.d_optimizer.apply_gradients(
            zip(grads, self.discriminator.trainable_weights)
        )

        # Assemble labels that say "all real images"
        misleading_labels = tf.zeros((batch_size, 1))

        # Train the generator (note that we should *not* update the weights
        # of the discriminator)!
        with tf.GradientTape() as tape:
          generated_vis_mass = self.generator(dnn_train)
          fake_vismass_labels = tf.concat([generated_vis_mass,fake_labels],-1)
          predictions = self.discriminator(fake_vismass_labels)
          g_loss_1 = self.g_loss_weight * self.loss_fn(misleading_labels, predictions)
          g_loss_2 = self.g_loss_weight * self.gen_loss_fn(real_vis_mass,generated_vis_mass)
          g_loss =g_loss_1 + g_loss_2
        #grads_gen = tape.gradient(gen_loss, self.generator.trainable_weights)
        grads = tape.gradient(g_loss, self.generator.trainable_weights)
        #grads_tot = grads + grads_gen
        self.g_optimizer.apply_gradients(zip(grads, self.generator.trainable_weights))
        # Update metrics
        self.d_loss_metric.update_state(d_loss)
        self.g_loss_metric.update_state(g_loss)
        return {
            "d_loss": self.d_loss_metric.result(),
            "g_loss": self.g_loss_metric.result(),
            "g_loss_loss": g_loss_1,
        }