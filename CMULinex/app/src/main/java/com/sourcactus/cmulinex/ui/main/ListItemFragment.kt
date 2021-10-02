package com.sourcactus.cmulinex.ui.main

import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.TextView
import androidx.fragment.app.Fragment
import androidx.lifecycle.Observer
import androidx.lifecycle.ViewModelProviders
import com.sourcactus.cmulinex.R

class ListItemFragment: Fragment() {
    private lateinit var pageViewModel: ListingViewModel

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        val namesList = this.resources.getStringArray(R.array.restaurants_array)
        pageViewModel = ViewModelProviders.of(this).get(ListingViewModel::class.java).apply {
            val index = arguments?.getInt(ARG_RESTAURANT_NUMBER) ?: 0
            setIndex(index)
            setTime(arguments?.getDouble(ARG_RESTAURANT_TIME) ?: 0.0)
            setName(namesList[index])
        }
    }

    override fun onCreateView(
        inflater: LayoutInflater, container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View? {
        val root = inflater.inflate(R.layout.fragment_listitem, container, false)
        val textView: TextView = root.findViewById(R.id.restaurant)
        pageViewModel.nameInfo.observe(this, Observer<String> {
            textView.text = it
        })
        return root
    }

    companion object {
        /**
         * The fragment argument representing the section number for this
         * fragment.
         */
        private const val ARG_RESTAURANT_NUMBER = "restaurant_number"
        private const val ARG_RESTAURANT_TIME = "restaurant_time"

        /**
         * Returns a new instance of this fragment for the given section
         * number.
         */
        @JvmStatic
        fun newInstance(restaurantNumber: Int, restaurantTime: Double): ListItemFragment {
            return ListItemFragment().apply {
                arguments = Bundle().apply {
                    putInt(ARG_RESTAURANT_NUMBER, restaurantNumber)
                    putDouble(ARG_RESTAURANT_TIME, restaurantTime)
                }
            }
        }
    }
}