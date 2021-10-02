package com.sourcactus.cmulinex.ui.main

import androidx.lifecycle.LiveData
import androidx.lifecycle.MutableLiveData
import androidx.lifecycle.Transformations
import androidx.lifecycle.ViewModel
import androidx.lifecycle.ViewModelProvider

class PageViewModel : ViewModel() {

    private val _index = MutableLiveData<Int>()
    private val _name = MutableLiveData<String>()
    private val _time = MutableLiveData<Double>()
    val text: LiveData<String> = Transformations.map(_index) {
        "Hello world from, section: $it"
    }

    fun setIndex(index: Int) {
        _index.value = index
    }


}