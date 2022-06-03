package com.example.ch11

import androidx.lifecycle.MutableLiveData
import androidx.lifecycle.ViewModel

data class Item(val name: String, val name2: String)
enum class ItemNotify {
    ADD, DELETE, UPDATE
}

class MyViewModel : ViewModel() {

    val itemsLiveData = MutableLiveData<ArrayList<Item>>()

    private val items = ArrayList<Item>()
    var longClickItem: Int = -1

    init {
        addItem(Item("John", "Appleseed"))
        addItem(Item("Aksidion", "Kreimben"))
    }

    var itemNotified: Int = -1
    val itemClickEvent = MutableLiveData<Int>()
    var itemNotifiedType: ItemNotify = ItemNotify.ADD

    fun getItem(pos: Int): Item = this.items[pos]

    fun getSize(): Int = this.items.size

    fun addItem(item: Item) {
        this.itemNotifiedType = ItemNotify.ADD
        this.itemNotified = -1

        this.items.add(item)
        this.itemsLiveData.value = this.items
    }

    fun updateItem(item: Item, pos: Int) {
        this.itemNotifiedType = ItemNotify.UPDATE
        this.itemNotified = pos

        this.items[pos] = item
        this.itemsLiveData.value = this.items
    }

    fun deleteItem(pos: Int) {
        this.itemNotifiedType = ItemNotify.DELETE
        this.itemNotified = pos

        this.items.removeAt(pos)
        this.itemsLiveData.value = this.items
    }
}