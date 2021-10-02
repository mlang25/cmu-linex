package com.sourcactus.cmulinex.ui.main

import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.LinearLayout
import android.widget.ListView
import android.widget.TextView
import androidx.fragment.app.Fragment
import androidx.lifecycle.Observer
import androidx.lifecycle.ViewModelProviders
import com.android.volley.Request
import com.android.volley.RequestQueue
import com.android.volley.Response
import com.android.volley.toolbox.*
import com.sourcactus.cmulinex.R

class ListingFragment: Fragment() {
    private lateinit var pageViewModel: PageViewModel
    private lateinit var reqQueue: RequestQueue

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        pageViewModel = ViewModelProviders.of(this).get(PageViewModel::class.java).apply {
            setIndex(arguments?.getInt(ARG_SECTION_NUMBER) ?: 1)
        }
    }

    override fun onCreateView(
        inflater: LayoutInflater, container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View? {
        reqQueue = Volley.newRequestQueue(this.context)
        val root = inflater.inflate(R.layout.fragment_listing, container, false)
        /*
        val textView: TextView = root.findViewById(R.id.section_label)
        pageViewModel.text.observe(this, Observer<String> {
            textView.text = it
        })
         */

        val header: TextView = root.findViewById(R.id.header)
        val mainLayout: LinearLayout = root.findViewById(R.id.main_layout)
        updateTimes(mainLayout, this)

        return root
    }

    fun updateTimes(view: LinearLayout, fragment: ListingFragment) {
        val url = "https://learning-backend.namanmansukhani.repl.co/send"
        val namesList: Array<String> = view.context.resources.getStringArray(R.array.restaurants_array)
        val jsonObjectRequest = JsonObjectRequest(
            Request.Method.GET, url, null,
            { response ->
                System.out.println("EEEEEK " + response.toString())
                val keys = response.keys()
                while(keys.hasNext()) {
                    val key = keys.next()
                    val keyNum = Integer.parseInt(key)
                    val ft = childFragmentManager.beginTransaction()
                    val value = response.getDouble(key)
                    val item:Fragment = ListItemFragment.newInstance(keyNum, value)
                    ft.add(R.id.main_layout, item)
                    ft.commitAllowingStateLoss()

                }
            },
            { error ->
                // TODO: Handle error
            }
        )
        reqQueue.add(jsonObjectRequest)

        /*
        for(i in 1..3) {
            val t = TextView(view.context)
            t.textSize = 20f
            t.text = "LINE $i!!!"
            view.addView(t)
        }

         */

    }

    companion object {
        /**
         * The fragment argument representing the section number for this
         * fragment.
         */
        private const val ARG_SECTION_NUMBER = "section_number"

        /**
         * Returns a new instance of this fragment for the given section
         * number.
         */
        @JvmStatic
        fun newInstance(sectionNumber: Int): ListingFragment {
            return ListingFragment().apply {
                arguments = Bundle().apply {
                    putInt(ARG_SECTION_NUMBER, sectionNumber)
                }
            }
        }
    }
}